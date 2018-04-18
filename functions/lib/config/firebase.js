"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const firebase = require("firebase-admin");
exports.fb = firebase.initializeApp({
    credential: firebase.credential.applicationDefault(),
    databaseURL: "https://next-001.firebaseio.com"
});
//# sourceMappingURL=firebase.js.map