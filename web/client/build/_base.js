const HtmlWebpackPlugin = require('html-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader')
const webpack = require('webpack');

const path = require('path')
const resolve = (dir) => path.join(__dirname, '..', dir)

module.exports = {
    entry: {
        main: './src/main.js',
        // joystick: './node_modules/html5-joystick/joy.js',
    },
    module: {
        rules: [{
            test: /\.css$/i,
            use: ['style-loader', 'css-loader', 'postcss-loader'],
        }, {
            test: /\.scss$/i,
            use: ['style-loader', 'css-loader', 'postcss-loader', "sass-loader"],
        }, {
            test: /\.vue$/i,
            use: 'vue-loader'
        }, {
            test: /\.(png|svg)$/,
            type: 'asset/resource'
        }, 
        ]
    },
    resolve: {
        alias: {
            '@': resolve('src'),
            'A': resolve('assets'),
        },
    },
    plugins: [
        // new CopyWebpackPlugin({
        //     patterns: [
        //         { from: 'data', to: 'data' },
        //     ]
        // }),
        new HtmlWebpackPlugin({
            template: 'index.html',
            favicon: 'assets/icon.png',
        }),
        new VueLoaderPlugin(),
        new webpack.DefinePlugin({ __VUE_PROD_DEVTOOLS__: 'false', }),
    ]
};
