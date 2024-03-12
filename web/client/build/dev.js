const baseConfig = require('./_base.js');
const { merge } = require('webpack-merge');

module.exports = merge(baseConfig, {
    mode: 'development',
    devServer: {
        historyApiFallback: {
            disableDotRule: true
        },
        open: true,
        liveReload: true,
        hot: false,
        port: 8000,
        allowedHosts: "all",
        proxy: [{
            context: ['/api'],
            target: {
                host: "localhost",
                protocol: 'http:',
                port: 8888
            },
            pathRewrite: {
                '^/api': ''
            }
        }],
    },
    devtool: 'source-map',
    output: {
        publicPath: '/'
    },
});
