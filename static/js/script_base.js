// ****************** Nav Bar hide ****************
let tab = [];
        let nav_barre = document.getElementById('nav_barre');
        window.addEventListener('scroll', () => {
            let y = window.scrollY;
            tab.push(y);
            if(tab[tab.length - 2] < window.scrollY){
                nav_barre.style.top = "-85px";
            }
            else{
                nav_barre.style.top = "0px";
            }
            if(tab[tab.length - 2] < window.scrollY  || window.scrollY != 0){
                nav_barre.style.background = "linear-gradient(135deg, #0a1f3c46, #1f3f7c46)";
            }
            else{
                nav_barre.style.background = "linear-gradient(135deg, #0a1f3c, #1f3f7c)";
            }
        });

// ****************** Social Media Footer************************
VanillaTilt.init(document.querySelectorAll('.sci li a'), {
  max: 25,
  speed: 400,
  glare: true,
  "max-glare": 1,
});
let list = document.querySelectorAll('.sci li');
let bg = document.querySelector('.paw');
list.forEach(elements  => {
    elements.addEventListener('mouseenter', function(event){
        let color = event.target.getAttribute('data-color');
        bg.style.background = color;
    });
    elements.addEventListener('mouseleave', function(event){
        bg.style.background = 'linear-gradient(135deg, #0a1f3c, #1f3f7c)';
    });
});
// ******************** Scroll to top *****************
const scrollUp = document.querySelector('.scrollUp');

window.addEventListener('scroll', () => {
    if(window.pageYOffset > 100){
        scrollUp.classList.add("active");
    }
    else{
        scrollUp.classList.remove("active");
    }
});

// ********************* Scroll Indicator **************
document.addEventListener("DOMContentLoaded", function () {
    var jq = jQuery.noConflict();

    // Lors du scroll de la page
    jq(window).on('scroll', function () {
        var wintop = jq(window).scrollTop();     // Position actuelle du scroll
        var docheight = jq(document).height();   // Hauteur totale du document
        var winheight = jq(window).height();     // Hauteur de la fenêtre visible

        // Pourcentage de scroll exprimé sur 126 unités
        var scrolled = (wintop / (docheight - winheight)) * 126;

        // Mise à jour de l'indicateur circulaire
        jq('#circleIndicator').css('stroke-dashoffset', -scrolled);
    });
});