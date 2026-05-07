class Presentation {
    constructor() {
        this.slides = document.querySelectorAll('.slide');
        this.currentIndex = -1; // Standard v4.7.1: Init with -1 to trigger first slide 
        this.totalSlides = this.slides.length;
        this.isAnimating = false;
        
        this.progressFill = document.getElementById('progress-fill');
        this.pageIndicator = document.getElementById('page-indicator');
        this.themeToggle = document.getElementById('theme-toggle');
        
        this.charts = {};
        
        this.init();
    }

    init() {
        // Initialize Lucide Icons
        if (window.lucide) {
            window.lucide.createIcons();
        }

        // Event Listeners
        window.addEventListener('hashchange', () => this.handleHash());
        window.addEventListener('keydown', (e) => this.handleKeydown(e));
        window.addEventListener('resize', () => this.initScaling());
        
        this.themeToggle.addEventListener('change', () => this.toggleTheme());
        
        // Help Modal
        const helpBtn = document.getElementById('help-btn');
        const helpModal = document.getElementById('help-modal');
        const closeHelp = document.getElementById('close-help');
        
        helpBtn.onclick = () => helpModal.classList.toggle('active');
        closeHelp.onclick = () => helpModal.classList.remove('active');
        
        // Initial setup
        this.initScaling();
        this.handleHash();
        this.initCharts();
        
        // Print synchronization (Standard v4.7.5)
        window.onbeforeprint = () => {
            const pres = document.getElementById('presentation');
            pres.style.transform = 'none';
            
            // Disable chart animations for static print
            Object.values(this.charts).forEach(chart => {
                chart.updateOptions({
                    chart: { animations: { enabled: false } }
                });
            });
        };

        window.onafterprint = () => {
            this.initScaling();
            
            // Re-enable chart animations
            Object.values(this.charts).forEach(chart => {
                chart.updateOptions({
                    chart: { animations: { enabled: true } }
                });
            });
        };
    }

    initScaling() {
        const presentation = document.getElementById('presentation');
        const baseWidth = 1400;
        const baseHeight = 787.5;
        
        const scaleX = window.innerWidth / baseWidth;
        const scaleY = window.innerHeight / baseHeight;
        const scale = Math.min(scaleX, scaleY) * 0.92; // 92% safe scale
        
        presentation.style.transform = `scale(${scale})`;
    }

    handleHash() {
        const hash = window.location.hash;
        const slideIndex = parseInt(hash.replace('#slide-', '')) || 0;
        this.goto(slideIndex);
    }

    goto(index) {
        if (index < 0 || index >= this.totalSlides || index === this.currentIndex || this.isAnimating) return;

        this.isAnimating = true;
        
        // Remove current class from all
        this.slides.forEach(s => s.classList.remove('current'));
        
        // Add to new
        this.slides[index].classList.add('current');
        this.currentIndex = index;
        
        // Update URL
        history.pushState(null, null, `#slide-${index}`);
        
        // Update UI
        this.updateUI();
        
        // Trigger Sequential Reveal
        this.triggerSteps();

        setTimeout(() => {
            this.isAnimating = false;
        }, 600);
    }

    next() {
        if (this.currentIndex < this.totalSlides - 1) {
            this.goto(this.currentIndex + 1);
        }
    }

    prev() {
        if (this.currentIndex > 0) {
            this.goto(this.currentIndex - 1);
        }
    }

    triggerSteps() {
        const currentSlide = this.slides[this.currentIndex];
        const steps = currentSlide.querySelectorAll('[data-step]');
        
        // Reset steps in other slides
        document.querySelectorAll('[data-step]').forEach(el => {
            if (!currentSlide.contains(el)) el.classList.remove('visible');
        });

        steps.forEach((step, i) => {
            setTimeout(() => {
                step.classList.add('visible');
            }, i * 300); // 0.3s interval
        });
    }

    updateUI() {
        const progress = ((this.currentIndex + 1) / this.totalSlides) * 100;
        this.progressFill.style.width = `${progress}%`;
        this.pageIndicator.innerText = `${(this.currentIndex + 1).toString().padStart(2, '0')} / ${this.totalSlides.toString().padStart(2, '0')}`;
    }

    toggleTheme() {
        const root = document.documentElement;
        const isDark = root.getAttribute('data-theme') === 'dark';
        const newTheme = isDark ? 'light' : 'dark';
        root.setAttribute('data-theme', newTheme);
        this.updateChartsTheme(newTheme);
    }

    handleKeydown(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        switch(e.key.toLowerCase()) {
            case 'arrowright':
            case ' ':
                this.next();
                break;
            case 'arrowleft':
            case 'backspace':
                this.prev();
                break;
            case 'h':
                this.goto(0);
                break;
            case 'p':
                this.exportPDF();
                break;
            case 't':
                this.themeToggle.checked = !this.themeToggle.checked;
                this.toggleTheme();
                break;
            case '?':
            case '/':
                document.getElementById('help-modal').classList.toggle('active');
                break;
            case 'escape':
                document.getElementById('help-modal').classList.remove('active');
                break;
        }
    }

    initCharts() {
        // Efficiency Chart (Bar)
        const effOptions = {
            series: [{
                name: 'Traditional Coding',
                data: [44, 55, 41, 67, 22]
            }, {
                name: 'VibeCoding',
                data: [113, 132, 133, 148, 98]
            }],
            chart: {
                type: 'bar',
                height: '100%',
                toolbar: { show: false },
                animations: { enabled: true, easing: 'easeinout', speed: 1000 },
                foreColor: 'var(--text-dim)'
            },
            plotOptions: {
                bar: { horizontal: false, columnWidth: '55%', borderRadius: 8 }
            },
            dataLabels: { enabled: false },
            colors: ['var(--slate-400)', 'var(--amber-500)'],
            xaxis: {
                categories: ['Frontend', 'Backend', 'Review', 'DevOps', 'Data'],
            },
            legend: { position: 'top', horizontalAlign: 'right' },
            grid: { borderColor: 'var(--glass-border)' }
        };

        this.charts.efficiency = new ApexCharts(document.querySelector("#efficiency-chart"), effOptions);
        this.charts.efficiency.render();

        // Quality Chart (RadialBar)
        const qualOptions = {
            series: [85, 92],
            chart: {
                height: 450,
                type: 'radialBar',
                foreColor: 'var(--text-dim)'
            },
            plotOptions: {
                radialBar: {
                    dataLabels: {
                        name: { fontSize: '22px' },
                        value: { fontSize: '16px' },
                        total: {
                            show: true,
                            label: 'SuccessRate',
                            formatter: function (w) { return 'High' }
                        }
                    },
                    track: { background: 'var(--glass-border)' }
                }
            },
            labels: ['Accuracy', 'Reliability'],
            colors: ['var(--amber-500)', 'var(--slate-400)']
        };

        this.charts.quality = new ApexCharts(document.querySelector("#quality-chart"), qualOptions);
        this.charts.quality.render();
    }

    updateChartsTheme(theme) {
        Object.values(this.charts).forEach(chart => {
            chart.updateOptions({
                theme: { mode: theme }
            });
        });
    }

    exportPDF() {
        // High stability print call
        window.print();
    }
}

// Global instance
const pres = new Presentation();
window.pres = pres;
