var colors = ['5DA5DA', 'FAA43A', '60BD68', 'F17CB0',
              'B2912F', 'B276B2', 'DECF3F', 'F15854', '4D4D4D'];

function getColor(index) {
    if (index < colors.length) {
        return '#' + colors[index]
    }
    else {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
}