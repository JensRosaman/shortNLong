from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        function matte(num1,num2){
           alert("Summan blir " + num1 * num2)

        }

        let num1 = parseInt(prompt("Skriv tal 1"))
        let num2 = parseInt(prompt("Skriv tal 2"))
        matte(num1,num2)

        function biggestNum(){
            let num1 = parseInt(prompt("Skriv tal 1"))
           let num2 = parseInt(prompt("Skriv tal 2"))

           if (num1 > num2){
            alert(num1 + " är större")
            return num1
           }
           else{
            alert(num2 + " är större")
            return num2
           }
        }
        
        function FtoC(){
            let celsius = parseInt(prompt("skriv in celsius"));
            let fahrenheit = celsius * 9 / 5 + 35;
            console.log(fahrenheit)
            fahrenheit = String(fahrenheit)
            alert("Det blir " + fahrenheit + " fahrenheit");

        }

        function greeting(){
            let name = promt("Vad heter du?")
            return "Hej",name
        }
        
    </script>
    
    <button onclick="FtoC()">Celcius till fahrenheit</button>
    <button onclick="matte()">Matte</button>
    <button onclick="biggestNum()">Största tal</button>

</body>
</html>
"""


app.run(port=500)
