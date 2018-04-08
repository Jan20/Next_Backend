import * as functions from 'firebase-functions'
import * as express from 'express'
import * as firebase from 'firebase-admin'
import * as request from 'request'

const firebaseApp = firebase.initializeApp({
	credential: firebase.credential.applicationDefault(),
	databaseURL: "https://next-001.firebaseio.com"
})

const express_app = express()

function getStocks(): any {
	const assetDocument: any = firebaseApp.firestore().doc(`/users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi`)
	const assetCollection: any = firebaseApp.firestore().collection(`/users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi/series`)
	assetDocument.get().then( doc => {
		
		console.log(doc.data().symbol)

		const assetName = doc.data().name
		const assetSymbol = doc.data().symbol

		request('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ETR:BMW&outputsize=compact&apikey=6404', function (error, response, body) {
		if (!error && response.statusCode === 200) {
			const data = JSON.parse(body)
		
			for (const key in data['Time Series (Daily)']) {
				
					if (data['Time Series (Daily)'].hasOwnProperty(key)) {
		
						console.log('____________________________________________________')
						console.log(assetName)
						console.log(data['Meta Data']['2. Symbol'])
						console.log(data['Time Series (Daily)'][key]['4. close'])
						console.log(key)
						console.log('____________________________________________________')

						assetCollection.add({
							'name': assetName,
							'symbol': data['Meta Data']['2. Symbol'],
							'close': data['Time Series (Daily)'][key]['4. close'],
							'date': key,
						})

					} else {
		
						console.log('Market data could not have been fetched')
						return;
					}
				}
			}
		})
	})
}


express_app.get("*", (req, res) => {
	getStocks()
	res.send('function has been executed')
})

export const stocks = functions.https.onRequest((req, res) => {

	!req.path ? req.url = `/${req.url}` : null
	return express_app(req, res)

});








///////////////
  // Functions //
  ///////////////
//   public getMarket(market: string): void {

//     for (let i = 1; i < this.seeds.length; i++) {
        
//       this.httpClient.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + this.seeds[i].getSymbol() +
//       '&outputsize=compact&apikey=6404')
//         .subscribe(data => {
//           this.timeline = new Timeline();
//           for (const key in data['Time Series (Daily)']) {
            
//             if (data['Time Series (Daily)'].hasOwnProperty(key)) {

//               this.stock = new Stock();
//               this.stock.setName(this.seeds[i].getName());
//               this.stock.setSymbol(data['Meta Data']['2. Symbol']);
//               this.stock.setClose(data['Time Series (Daily)'][key]['4. close']);
//               this.stock.setDate(key);
//               this.timeline.getStocks().push(this.stock);

//             } else {

//               alert('Market data could not have been fetched');
//               return;

//             }

//           }
//           console.log(this.timeline);
//           for (let j = 0; j < 12; j++) {
            
//             const stock = this.timeline.getStocks()[j];

//             stock.setChange(
//               (this.timeline.getStocks()[j].getClose() -
//                 this.timeline.getStocks()[j + 1].getClose() ) /
//                 this.timeline.getStocks()[j + 1].getClose()
//               );
//             this.angularFireDatabase.object('Dax' + '/' + this.seeds[i].getName() + '/' + stock.getDate()).set(stock);
//           }
//       });
//     }

//   }