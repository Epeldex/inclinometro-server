
let intervalData;
let intervalDiscover;
const selectValue = document.getElementById('mySelect');
console.log(selectValue)
async function dowork() {
    var selectedValue = selectValue.value;
    if (typeof selectValue !== 'undefined') {
        for (var i = selectValue.options.length; i >= 1; i--) {
            if (selectedValue != selectValue.options[i]) {
                selectValue.remove(i);
            }
        }
    }
    options = await fetchDevices();
    options = quitarDigitos(options)
    addOptions(options);
}

function quitarDigitos(string) {
    return string.slice(2, -2);
}

async function fetchDevices() {
    response = await fetch("/devices");
    return response.ok ? response.text() : null;
}

function addOptions(options) {
    var selectElement = document.querySelector('.select select');
    var newOption = document.createElement('option');
    newOption.value = options;
    newOption.text = options;
    selectElement.appendChild(newOption);
}
intervalDiscover = setInterval(dowork, 5000);


async function sendDevice(selectedValue) {
    await fetch("/select_device/" + selectedValue);
}

selectValue.addEventListener('change', function (event) {
    if (intervalData !== undefined) {
        clearInterval(intervalData);
    }
    var selectedValue = selectValue.value;
    sendDevice(selectedValue);
    intervalData = setInterval(refreshData, 5000);
});

function refreshData() {
    console.log(takeData())
}

async function takeData() {
    var selectedValue = selectValue.value;
    response = await fetch("/refresh_data/" + selectedValue);
    return response.ok ? response.text() : null;
}