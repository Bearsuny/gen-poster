var main = {
    getPixelRatio: function (context) {
        var backingStore = context.backingStorePixelRatio ||
            context.webkitBackingStorePixelRatio ||
            context.mozBackingStorePixelRatio ||
            context.msBackingStorePixelRatio ||
            context.oBackingStorePixelRatio ||
            context.backingStorePixelRatio || 1;
        return (window.devicePixelRatio || 1) / backingStore;
    },

    html2Canvas: function () {
        var content = document.getElementById('origin');
        var width = content.offsetWidth;
        var height = content.offsetHeight;
        var offsetTop = content.offsetTop;

        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        var scaleBy = main.getPixelRatio(context);
        canvas.width = width * scaleBy;
        canvas.height = (height + offsetTop) * scaleBy;
        context.scale(scaleBy, scaleBy);

        var opts = {
            allowTaint: true,
            tainttest: true,
            scale: scaleBy,
            canvas: canvas,
            logging: false,
            width: width,
            height: height
        };
        html2canvas(content, opts).then(function (canvas) {
            document.getElementById('generate').appendChild(canvas);
            canvas.setAttribute('id', 'canvas');
        });
    },

    canvas2Image: function () {
        canvas = document.getElementById('canvas');
        Canvas2Image.saveAsJPEG(canvas, 980, 1400)
    }
};
main.html2Canvas();
setTimeout(main.canvas2Image, 2000)