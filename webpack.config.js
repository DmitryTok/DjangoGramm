const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './static_src/main.js',
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'DjangoGramm/templates/base.html',
    }),
  ],
  devServer: {
    port: 8000,
  },
};
