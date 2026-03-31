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
    }
}