import { fb } from './../config/firebase'
import { User } from './../user/user-model'
import { Asset } from '../asset/asset-model';

export class PortfolioService {

	///////////////
	// Variables //
	///////////////
	private user: User
	private asset_rank: number[] = []

	///////////////
	// Functions //
	///////////////
	public rankAsset(asset: Asset) {

		// this.asset_rank = []

		// // const assetCollection: any = firebaseApp.firestore().collection(`/users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi/short_term_predictions_percentage`).get().then(entries => {
		// const assetCollection = fb.firestore().doc(`/users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi`).get().then(doc => {
	
		// 	doc.data().short_term_prediction
		// 	console.log(doc.data().short_term_prediction)
		// 	let expected_short_term_return = 0
	
		// })
	
	
	};
	
	
	


}

