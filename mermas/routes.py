from flask import render_template, request, jsonify
from . import mermas
from models import Insumo, db
from flask_security import login_required
from flask_security.decorators import roles_accepted
from sqlalchemy import text


@mermas.route('/mermas')
@login_required
@roles_accepted('Gerente', 'gerente')
def index():
    insumos = Insumo.query.filter_by(activo=True).order_by(Insumo.nombre).all()
    return render_template('mermas/index.html', insumos=insumos)


@mermas.route('/mermas/data')
@login_required
@roles_accepted('Gerente', 'gerente')
def data():
    """Return JSON with merma series from view v_merma_por_mes.
    Query params: insumo_id (int, 0=all), start (YYYY-MM), end (YYYY-MM)
    """
    insumo_id = int(request.args.get('insumo_id', 0))
    start = request.args.get('start')
    end = request.args.get('end')

    # normalize dates to YYYY-MM-01
    if start:
        start_period = f"{start}-01" if len(start) == 7 else start
    else:
        start_period = None
    if end:
        end_period = f"{end}-01" if len(end) == 7 else end
    else:
        end_period = None

    # Build base SQL for v_merma_por_mes. Detect actual column names in the view
    base_where = " WHERE 1=1"
    params = {}
    # Inspect INFORMATION_SCHEMA to find available columns on the view
    try:
        conn_info = db.engine.connect()
        schema_name = db.engine.url.database
        col_sql = text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = :schema AND TABLE_NAME = 'v_merma_por_mes'")
        col_res = conn_info.execute(col_sql, {'schema': schema_name})
        cols = [r[0] for r in col_res]
        conn_info.close()
    except Exception:
        cols = []

    # Decide which merma column exists
    if 'merma_real' in cols:
        select_candidates = ["SELECT id_insumo, nombre, periodo, total_comprado, merma_real AS total_merma FROM v_merma_por_mes"]
    elif 'total_merma' in cols:
        select_candidates = ["SELECT id_insumo, nombre, periodo, total_comprado, total_merma FROM v_merma_por_mes"]
    else:
        # fallback: try both variants (older/newer view names)
        select_candidates = [
            "SELECT id_insumo, nombre, periodo, total_comprado, merma_real AS total_merma FROM v_merma_por_mes",
            "SELECT id_insumo, nombre, periodo, total_comprado, total_merma FROM v_merma_por_mes"
        ]
    sql = None
    rows = []
    last_exc = None
    for select_sql in select_candidates:
        try:
            candidate = select_sql + base_where
            # build fresh params for each candidate to avoid cross-contamination
            local_params = {}
            if insumo_id and insumo_id > 0:
                candidate += " AND id_insumo = :insumo_id"
                local_params['insumo_id'] = insumo_id
            if start_period:
                candidate += " AND periodo >= :start"
                local_params['start'] = start_period
            if end_period:
                candidate += " AND periodo <= :end"
                local_params['end'] = end_period
            candidate += " ORDER BY id_insumo, periodo"

            # use session.execute with .mappings().all() for dict-like rows
            result = db.session.execute(text(candidate), local_params)
            mapped = result.mappings().all()
            rows = [dict(r) for r in mapped]
            sql = candidate
            break
        except Exception as e:
            # save and try next candidate
            last_exc = e
            # continue to next candidate
            continue

    if sql is None:
        import traceback
        tb = traceback.format_exc()
        return jsonify({'error': str(last_exc), 'trace': tb}), 500

    # Group by insumo and build series
    from collections import defaultdict, OrderedDict
    group = defaultdict(OrderedDict)
    periods_set = set()
    name_map = {}
    for r in rows:
        periods_set.add(r['periodo'].strftime('%Y-%m-01') if hasattr(r['periodo'], 'strftime') else str(r['periodo']))
        key = int(r['id_insumo'])
        name_map[key] = r['nombre']
        group[key][str(r['periodo'])] = {
            'total_comprado': float(r['total_comprado'] or 0),
            'total_merma': float(r['total_merma'] or 0)
        }

    # Build ordered list of periods
    periods = sorted(list(periods_set))

    datasets = []
    for insumo_id_k, series in group.items():
        comprado = []
        merma = []
        acumulado_merma = []
        ac = 0.0
        for p in periods:
            v = series.get(p)
            tcomp = v['total_comprado'] if v else 0.0
            tmer = v['total_merma'] if v else 0.0
            comprado.append(tcomp)
            merma.append(tmer)
            ac += tmer
            acumulado_merma.append(ac)
        datasets.append({
            'insumo_id': insumo_id_k,
            'nombre': name_map.get(insumo_id_k, ''),
            'comprado': comprado,
            'merma': merma,
            'acumulada': acumulado_merma
        })

    return jsonify({
        'periods': periods,
        'datasets': datasets
    })
