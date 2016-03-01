module.exports = {
    entry: "./lso/texts/static/js/texts-app.js",
    output: {
        path: __dirname,
        filename: "./lso/static/gen/texts-app.js"
    },
    module: {
        loaders: [
            {
                test    : /\.jsx?$/,
                loader  : 'babel-loader',
                exclude : /node_modules/,
                query   : {
                    presets: ['es2015', 'react'],
                }
            },
        ],
    },
};
