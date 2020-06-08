"use strict";

const lanIP = `${window.location.hostname}:5000`;
const endPoint = `http://${lanIP}/api/v1`; 


//#region ***  DOM references ***
//#endregion

//#region ***  Random functions ***
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showOpenAuctions = function(jsonObject) {
    console.log(jsonObject);

    htmlString = '';

    for(const autcion of jsonObject.auctions) {
        htmlString += `
        <h2>test</h2>
        <p>
            Sed lorem ipsum dolor sit amet nullam consequat feugiat consequat magna
            adipiscing magna etiam amet veroeros. Lorem ipsum dolor tempus sit cursus.
            Tempus nisl et nullam lorem ipsum dolor sit amet aliquam.
        </p>
        <ul class="actions">
            <li><a href="generic.html" class="button">Historiek</a></li>
        </ul>
        `;
    }
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
const callbackErrorFetch = function(jsonObject) {
    console.log(jsonObject);
}
//#endregion

//#region ***  Data Access - get___ ***
const getOpenAuctions = function() {
    handleData(`${endPoint}/get_auctions/`, showOpenAuctions, callbackErrorFetch);
}
//#endregion

//#region ***  Event Listeners - listenTo___ ***
const listenToUI = function() {
    for(const htmlCTA of document.querySelectorAll('.js-wash-me')) {
        htmlCTA.addEventListener('click', function() {
            if (!htmlCTA.classList.contains('c-cta--disabled')) {
                console.log(htmlCTA.innerHTML);
                if (htmlCTA.querySelector('.c-link-cta').innerHTML === 'Wassen') {
                    window.location.href = `programma_selectie.html?mand=${this.getAttribute('data-basket')}`;
                }   else {
                    cancelWas(this.getAttribute('data-washistoriek-id'));
                }
            }   else {
                window.alert('TODO: Toch doorlaten naar programma\'s, maar die blokkeren met een langere duurtijd dan het huidig geschedulde programma, niet mvp');
            }
        })
    }
}
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const init = function() {
    console.log("DOM Content Loaded");
    listenToUI();
}
//#endregion

document.addEventListener("DOMContentLoaded", init);
