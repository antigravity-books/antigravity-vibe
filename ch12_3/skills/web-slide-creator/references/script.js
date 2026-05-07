/**
 * AI Leadership Presentation Engine - Script v3.5
 * Upgraded with ApexCharts for Premium Visualization
 */

class Presentation {
    constructor() {
        this.container = document.querySelector('.presentation');
        this.slides = Array.from(document.querySelectorAll('.slide'));
        this.progressBar = document.getElementById('progress-bar');
        this.slideNumberDisplay = document.getElementById('slide-number');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.homeBtn = document.getElementById('home-btn');
        this.themeToggle = document.getElementById('theme-toggle');

        this.currentIndex = 0;
        this.isAnimating = false;
        this.animationDuration = 700;
        this.revealTimers = [];
        
        // Charts Reference
        this.charts = {
            efficiency: null,
            accuracy: null,
            trend: null
        };

        // Sync Persisted State
        this.currentTheme = localStorage.getItem('presentation-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        this.currentPalette = localStorage.getItem('presentation-palette') || 'emerald';
        document.documentElement.setAttribute('data-palette', this.currentPalette);

        this.touchStartX = 0;
        this.touchEndX = 0;

        this.init();
    }

    init() {
        this.bindEvents();
        if (window.location.hash) {
            this.handleHashChange();
        } else {
            this.updateSlideState();
        }
        this.updateThemeVisuals();
        this.renderIcons();
        this.initCharts();
    }

    renderIcons() {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        } else {
            setTimeout(() => this.renderIcons(), 100);
        }
    }

    bindEvents() {
        // Keyboard Navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') this.next();
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'h' || e.key === 'H') this.goto(0);
            if (e.key === 'f' || e.key === 'F') this.toggleFullscreen();
        });

        // Click Controls
        if (this.prevBtn) this.prevBtn.addEventListener('click', () => this.prev());
        if (this.nextBtn) this.nextBtn.addEventListener('click', () => this.next());
        if (this.homeBtn) this.homeBtn.addEventListener('click', () => this.goto(0));

        // Swipe (Touch)
        if (this.container) {
            this.container.addEventListener('touchstart', (e) => {
                this.touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });
            this.container.addEventListener('touchend', (e) => {
                this.touchEndX = e.changedTouches[0].screenX;
                this.handleSwipe();
            }, { passive: true });
        }

        // Theme & Palette
        if (this.themeToggle) this.themeToggle.addEventListener('click', () => this.toggleTheme());
        document.querySelectorAll('.swatch').forEach(swatch => {
            swatch.addEventListener('click', () => {
                const palette = swatch.getAttribute('data-palette');
                this.changePalette(palette);
            });
        });

        window.addEventListener('hashchange', () => this.handleHashChange());
    }

    handleHashChange() {
        const hash = window.location.hash;
        if (hash) {
            const slideNum = parseInt(hash.replace('#slide-', ''), 10);
            if (!isNaN(slideNum) && slideNum > 0 && slideNum <= this.slides.length) {
                const targetIdx = slideNum - 1;
                if (this.currentIndex !== targetIdx) {
                    this.goto(targetIdx);
                } else if (this.revealTimers.length === 0) {
                    this.updateSlideState();
                }
            }
        }
    }

    handleSwipe() {
        const threshold = 50;
        if (this.touchEndX < this.touchStartX - threshold) this.next();
        if (this.touchEndX > this.touchStartX + threshold) this.prev();
    }

    goto(index) {
        if (index < 0 || index >= this.slides.length || (this.currentIndex === index && this.isAnimating)) return;
        this.currentIndex = index;
        this.updateSlideState();
    }

    next() {
        if (this.currentIndex < this.slides.length - 1) {
            this.currentIndex++;
            this.updateSlideState();
        }
    }

    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateSlideState();
        }
    }

    resetFragments(slide) {
        const steps = slide.querySelectorAll('[data-step]');
        steps.forEach(step => {
            step.style.transition = 'none';
            step.classList.remove('visible');
            void step.offsetHeight;
            step.style.transition = '';
        });
    }

    updateSlideState() {
        this.isAnimating = true;
        const currentHash = `slide-${this.currentIndex + 1}`;
        if (window.location.hash !== `#${currentHash}`) {
            window.location.hash = currentHash;
        }

        const nextSlide = this.slides[this.currentIndex];
        this.resetFragments(nextSlide);

        this.updateUI();
        this.autoRevealCurrentSlide();
        
        // Trigger Chart Animations if on Slide 13
        if (this.currentIndex === 12) {
            setTimeout(() => this.animateCharts(), 600);
        }

        setTimeout(() => {
            this.isAnimating = false;
        }, this.animationDuration);
    }

    autoRevealCurrentSlide() {
        while (this.revealTimers.length > 0) {
            clearTimeout(this.revealTimers.shift());
        }

        const activeSlide = this.slides[this.currentIndex];
        const steps = Array.from(activeSlide.querySelectorAll('[data-step]'));

        steps.forEach((step, idx) => {
            const timer = setTimeout(() => {
                step.classList.add('visible');
            }, 600 + (idx * 350)); 
            this.revealTimers.push(timer);
        });
    }

    updateUI() {
        this.slides.forEach((slide, idx) => {
            const isActive = idx === this.currentIndex;
            slide.classList.toggle('active', isActive);
            slide.classList.toggle('prev', idx < this.currentIndex);
        });

        const progress = ((this.currentIndex + 1) / this.slides.length) * 100;
        if (this.progressBar) this.progressBar.style.width = `${progress}%`;

        if (this.slideNumberDisplay) {
            this.slideNumberDisplay.textContent = `${(this.currentIndex + 1).toString().padStart(2, '0')} / ${this.slides.length.toString().padStart(2, '0')}`;
        }

        if (this.prevBtn) this.prevBtn.style.opacity = (this.currentIndex === 0) ? '0.2' : '1';
        if (this.nextBtn) this.nextBtn.style.opacity = (this.currentIndex === this.slides.length - 1) ? '0.2' : '1';
    }

    toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const target = current === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', target);
        localStorage.setItem('presentation-theme', target);
        this.currentTheme = target;
        
        this.updateThemeVisuals();
        this.updateChartsTheme();
    }

    updateThemeVisuals() {
        if (this.themeToggle) {
            const iconName = this.currentTheme === 'light' ? 'sun' : 'moon';
            this.themeToggle.innerHTML = `<i data-lucide="${iconName}"></i>`;
            this.renderIcons();
        }
    }

    changePalette(palette) {
        this.currentPalette = palette;
        document.documentElement.setAttribute('data-palette', palette);
        localStorage.setItem('presentation-palette', palette);
        document.querySelectorAll('.swatch').forEach(s => {
            s.classList.toggle('active', s.getAttribute('data-palette') === palette);
        });
        this.updateChartsTheme();
    }

    // --- Premium Visualization Logic (ApexCharts) ---
    
    getPaletteColor() {
        switch(this.currentPalette) {
            case 'emerald': return '#10b981';
            case 'indigo': return '#6366f1';
            case 'rose': return '#f43f5e';
            default: return '#10b981';
        }
    }

    initCharts() {
        const color = this.getPaletteColor();
        const fontColor = this.currentTheme === 'dark' ? '#94a3b8' : '#475569';

        // 1. Efficiency Chart (Bar)
        const effOptions = {
            series: [{ name: '증대율', data: [15, 45, 92] }],
            chart: { type: 'bar', height: 250, toolbar: { show: false }, animations: { speed: 1200 } },
            plotOptions: { bar: { borderRadius: 8, distributed: true, columnWidth: '60%' } },
            colors: [color + '66', color + 'CC', color],
            xaxis: { categories: ['비숙련', '단순 활용', '리더십'], labels: { style: { colors: fontColor, fontSize: '12px' } } },
            yaxis: { show: false },
            tooltip: { theme: this.currentTheme },
            grid: { show: false },
            dataLabels: { enabled: true, formatter: (val) => val + '%', style: { fontSize: '12px' } }
        };
        this.charts.efficiency = new ApexCharts(document.querySelector("#chart-efficiency"), effOptions);
        this.charts.efficiency.render();

        // 2. Accuracy Chart (RadialBar)
        const accOptions = {
            series: [85],
            chart: { type: 'radialBar', height: 250, animations: { speed: 1500 } },
            plotOptions: {
                radialBar: {
                    hollow: { size: '65%' },
                    dataLabels: {
                        name: { show: false },
                        value: { color: this.currentTheme === 'dark' ? '#fff' : '#000', fontSize: '30px', fontWeight: 800, offsetY: 10, offsetSetter: (val) => val + '%' }
                    }
                }
            },
            colors: [color],
            stroke: { lineCap: 'round' }
        };
        this.charts.accuracy = new ApexCharts(document.querySelector("#chart-accuracy"), accOptions);
        this.charts.accuracy.render();

        // 3. Trend Chart (Area)
        const trendOptions = {
            series: [{ name: '생산성', data: [31, 40, 58, 51, 82, 94] }],
            chart: { type: 'area', height: 250, toolbar: { show: false }, animations: { speed: 1800 } },
            dataLabels: { enabled: false },
            stroke: { curve: 'smooth', width: 3, colors: [color] },
            fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.5, opacityTo: 0.1, colorStops: [ { offset: 0, color: color, opacity: 0.5 }, { offset: 100, color: color, opacity: 0 } ] } },
            xaxis: { categories: ['1월', '2월', '3월', '4월', '5월', '6월'], labels: { style: { colors: fontColor } } },
            yaxis: { show: false },
            grid: { borderColor: this.currentTheme === 'dark' ? '#334155' : '#e2e8f0', strokeDashArray: 4 },
            tooltip: { theme: this.currentTheme }
        };
        this.charts.trend = new ApexCharts(document.querySelector("#chart-trend"), trendOptions);
        this.charts.trend.render();
    }

    animateCharts() {
        Object.values(this.charts).forEach(chart => {
            if(chart) chart.updateOptions({ chart: { animations: { enabled: true } } });
        });
    }

    updateChartsTheme() {
        const color = this.getPaletteColor();
        const fontColor = this.currentTheme === 'dark' ? '#94a3b8' : '#475569';

        this.charts.efficiency.updateOptions({
            colors: [color + '66', color + 'CC', color],
            xaxis: { labels: { style: { colors: fontColor } } },
            tooltip: { theme: this.currentTheme }
        });

        this.charts.accuracy.updateOptions({
            colors: [color],
            plotOptions: { radialBar: { dataLabels: { value: { color: this.currentTheme === 'dark' ? '#fff' : '#000' } } } }
        });

        this.charts.trend.updateOptions({
            stroke: { colors: [color] },
            fill: { gradient: { colorStops: [ { offset: 0, color: color, opacity: 0.5 }, { offset: 100, color: color, opacity: 0 } ] } },
            xaxis: { labels: { style: { colors: fontColor } } },
            grid: { borderColor: this.currentTheme === 'dark' ? '#334155' : '#e2e8f0' },
            tooltip: { theme: this.currentTheme }
        });
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

// Initialize on Load
window.addEventListener('DOMContentLoaded', () => {
    window.slides = new Presentation();
});
