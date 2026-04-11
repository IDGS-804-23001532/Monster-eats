from flask import render_template
from Pagina import pagina_bp
from models import Producto, CategoriaProducto

@pagina_bp.route('/menu/<categoria>', methods=['GET'])
def menu_categoria(categoria):
    # Buscamos la categoria ignorando mayusculas/minusculas
    cat = CategoriaProducto.query.filter(CategoriaProducto.nombre.ilike(categoria)).first()
    
    if not cat:
        productos = []
        nombre_cat = categoria.capitalize()
    else:
        # Filtramos los productos activos que pertenecen a esa categoría
        productos = Producto.query.filter_by(id_categoria=cat.id_categoria, activo=True).all()
        nombre_cat = cat.nombre

    # Renderizamos la plantilla dinámica Pasando los datos de la Base de Datos
    return render_template('Pagina/Productos.html', productos=productos, categoria_nombre=nombre_cat)
