import * as firebase from 'firebase-admin'

export const fb = firebase.initializeApp({
	credential: firebase.credential.applicationDefault(),
	databaseURL: "https://next-001.firebaseio.com"
})