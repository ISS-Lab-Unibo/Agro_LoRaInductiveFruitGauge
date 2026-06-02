function Decode(fPort, bytes, variables) {

    var Obj = {};

    // 8 pinze (uint16 / 100)
    Obj.pinza1 = roundTo(readUint16() / 100, 2);
    Obj.pinza2 = roundTo(readUint16() / 100, 2);
    Obj.pinza3 = roundTo(readUint16() / 100, 2);
    Obj.pinza4 = roundTo(readUint16() / 100, 2);
    Obj.pinza5 = roundTo(readUint16() / 100, 2);
    Obj.pinza6 = roundTo(readUint16() / 100, 2);
    Obj.pinza7 = roundTo(readUint16() / 100, 2);
    Obj.pinza8 = roundTo(readUint16() / 100, 2);

    // 4 ingressi analogici (uint16 / 10)
    Obj.analogico1 = roundTo(readUint16() / 10, 1);
    Obj.analogico2 = roundTo(readUint16() / 10, 1);
    Obj.analogico3 = roundTo(readUint16() / 10, 1);
    Obj.analogico4 = roundTo(readUint16() / 10, 1);

    Obj.battVoltage = roundTo(readUint16() / 100, 2);

    var jsonString = JSON.stringify(Obj);

    return jsonString;
}

/* Funzione per l'arrotondamento */
function roundTo(value, decimalpositions)
{
    var i = value * Math.pow(10, decimalpositions);
    i = Math.round(i);
    return i / Math.pow(10, decimalpositions);
}


    var index = 0;

    function readUint16() {
        var value = (bytes[index + 1] << 8) | bytes[index];
        index += 2;
        return value;
    }