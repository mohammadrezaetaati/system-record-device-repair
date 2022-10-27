let canvas = document.querySelector('#myBarChart');
let canvasWidth = document.querySelector('.mos-chart').clientWidth;
let canvasHeight = canvas.height;
canvas.style.width = "100%";
canvas.style.height = "100%";
canvas.width = canvasWidth;
let entry = 100;

const ctx = canvas.getContext('2d');

class Chart {

    constructor({ labels = [
        {
            name: 'فروردین',
            data: 100
        },
        {
            name: 'اردیبهشت',
            data: 200
        },
        {
            name: 'خرداد',
            data: 40
        },
        {
            name: 'تیر',
            data: 36
        },
        {
            name: 'مرداد',
            data: 100
        },
        {
            name: 'شهریور',
            data: 100
        },
        {
            name: 'مهر',
            data: 100
        },
        {
            name: 'آبان',
            data: 250
        },
        {
            name: 'آذر',
            data: 100
        },
        {
            name: 'دی',
            data: 100
        },
        {
            name: 'بهمن',
            data: 100
        },
        {
            name: 'اسفند',
            data: 100
        },

    ], colors = ['#0ad747', '#f72929'], numbers = 50, maxNumber = 500, data = [] }) {
        this.labels = labels;
        this.colors = colors;
        this.numbers = numbers;
        this.maxNumber = maxNumber;
        this.data = data;

        this.drawChart();
    }

    drawChart = () => {

        ctx.beginPath();
        this.labels.forEach((item, index) => {
            ctx.fillStyle = this.colors[0];
            ctx.fillRect(((canvasWidth / 12 - 10) * index) + 10, canvasHeight - (canvasHeight * item.data) / this.maxNumber, 50, (canvasHeight * item.data) / this.maxNumber);
            ctx.fillStyle = this.colors[1];
            ctx.fillRect(((canvasWidth / 12 - 10) * index) + 65, canvasHeight - (canvasHeight * item.data) / this.maxNumber, 50, (canvasHeight * item.data) / this.maxNumber);
        })


        ctx.closePath();

    }


}

new Chart({});