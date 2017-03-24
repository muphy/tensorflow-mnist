from flask import Flask, jsonify, render_template, request

from funcbox import tf_package


# webapp
app = Flask(__name__)

@app.route('/api/packages/price', methods=['GET'])
def hello():
    pop_id = request.args.get('pop_id')
    if len(pop_id) != 4:
        return jsonify(results="bad request: pop_id")
    cover_code = request.args.get('cover_code')
    if len(cover_code) != 22:
        return jsonify(results="bad request: cover_code")
    if pop_id is None:
        age = float(request.args.get('price'))/10
        job = request.args.get('job')
        gender = request.args.get('gender')
    else:
        age = float(pop_id[:2])/10
        job = pop_id[2:3]
        gender = pop_id[-1]
    package_price = tf_package.calc_package_price(age,job,gender,cover_code)
    res = {
       'price':package_price
    }
    # print(res)
    return jsonify(results=res)

@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    # app.run()
# app.run(host='0.0.0.0', port=app.config["PORT"], debug=app.config["DEBUG"])
    app.config.update(
        TEMPLATES_AUTO_RELOAD=True
    )
    app.run(host='0.0.0.0', port=9998, debug=False)