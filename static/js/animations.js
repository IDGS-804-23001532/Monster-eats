const MonsterAnimations = {
    // Animacion de entrada del login
    animateLogin: function() {
        if (document.querySelector('.login-box')) {
            gsap.fromTo(".login-box",
                { y: 50, opacity: 0 },
                { y:0, opacity: 1, duration: 0.8, ease: "power3.out" }
            );

            gsap.fromTo(".anim-item", 
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power2.out", delay: 0.2 }
            );
        }
    },

    // Animación global para mensajes de error/éxito (Reutilizable en todo el sistema)
    animateFlashMessages: function() {
        const flashMessages = document.querySelectorAll(".flash-message");
        if (flashMessages.length > 0) {
            gsap.fromTo(".flash-message", 
                { y: -30, opacity: 0 }, 
                { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: "back.out(1.7)" }
            );

            // Si estamos en el login, hacemos la sacudida de negación
            if (document.querySelector('.login-box')) {
                gsap.to(".login-box", {
                    x: "random(-10, 10)",
                    duration: 0.1,
                    yoyo: true,
                    repeat: 5,
                    delay: 0.3
                });
            }
        }
    },

    // Animación de entrada general para cuando cambias de página
    animatePageEntry: function() {
        const mainContent = document.querySelector('main');
        if (mainContent) {
            gsap.fromTo(mainContent, 
                { opacity: 0, y: 15 }, 
                { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }
            );
        }
    },

    animateModals: function() {
        // Escuchamos todos los clics que ocurran en el documento
        document.addEventListener('click', (event) => {
            // Buscamos si el clic fue en un botón con id="button-animate" o dentro de él
            const button = event.target.closest('.btn-animate-modal');
            
            if (button) {
                // Leemos a qué modal quiere abrir este botón
                const modalId = button.getAttribute('data-modal-target');
                if (modalId) {
                    // Buscamos la "caja interna" de ese modal específico para animarla
                    const modalBox = document.querySelector(`#${modalId} > div > div`);
                    
                    if (modalBox) {
                        // Le damos la animación de rebote y opacidad
                        gsap.fromTo(modalBox, 
                            { 
                                opacity: 0, 
                                y: -40,
                                scale: 0.95 
                            }, 
                            { 
                                opacity: 1, 
                                y: 0, 
                                scale: 1, 
                                duration: 0.4, 
                                ease: "back.out(1.2)" 
                            }
                        );
                    }
                }
            }
        });
    }
}