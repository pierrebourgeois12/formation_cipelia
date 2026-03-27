// Smooth scroll navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all skill cards and experience cards
document.querySelectorAll('.skill-category, .project-card, .role-card, .stat').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Add scroll class to navbar
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.boxShadow = 'var(--shadow)';
    }
});

// Contact form validation (if needed in future)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Counter animation for stats
function animateCounters() {
    const stats = document.querySelectorAll('.stat h3');
    const speed = 30;
    
    stats.forEach(stat => {
        const target = parseInt(stat.textContent);
        if (isNaN(target)) return;
        
        const increment = target / speed;
        let current = 0;
        
        const updateCount = () => {
            current += increment;
            if (current < target) {
                stat.textContent = Math.ceil(current) + '+';
                setTimeout(updateCount, 30);
            } else {
                stat.textContent = target + '+';
            }
        };
    });
}

// Trigger counter animation when stats section comes into view
const statsSection = document.querySelector('.about');
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

if (statsSection) {
    statsObserver.observe(statsSection);
}

// Responsive navigation menu toggle for mobile
function setupMobileMenu() {
    const navbar = document.querySelector('.navbar');
    const navMenu = document.querySelector('.nav-menu');
    
    if (window.innerWidth <= 768) {
        // Mobile menu functionality could be added here
        console.log('Mobile menu setup ready');
    }
}

setupMobileMenu();

// Rerun setup on resize
window.addEventListener('resize', setupMobileMenu);

// Log that the script has loaded
console.log('Portfolio script loaded successfully');
