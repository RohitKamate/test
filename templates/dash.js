// static/dash.js
const dashApp = new Dash({
    requestQueue: true,
    inputs: [],
    outputs: [],
    onUpdate: []
});

dashApp.layout(document.getElementById('my-graph'));
