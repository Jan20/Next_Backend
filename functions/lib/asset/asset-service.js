"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const firebase_1 = require("../config/firebase");
const asset_model_1 = require("./asset-model");
const request = require("request");
class AssetService {
    //////////////////
    // Constructors //
    //////////////////
    // public constructor() {}
    ///////////////
    // Functions //
    ///////////////
    fetchAssetsFromAlphaVantage(userId, marketId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.fetchAssets(userId, marketId);
            console.log(userId);
            console.log(marketId);
            console.log(this.assets);
            this.assets.forEach(asset => this.fetchAssetFromAlphaVantage(userId, marketId, asset));
        });
    }
    /*
    *
    *	Simple function to access the Alpha Vantage API, make a call and write all relevant datapoints back
    *	into a Firestore realtime database
    *
    */
    fetchAssetFromAlphaVantage(userId, marketId, asset) {
        return __awaiter(this, void 0, void 0, function* () {
            yield request(`https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${asset.symbol}&outputsize=compact&apikey=6404`, function (error, response, body) {
                if (error && response.statusCode !== 200) {
                    console.log('Asset data could not have been retrieved.');
                    return;
                }
                const data = JSON.parse(body);
                for (const key in data['Time Series (Daily)']) {
                    if (data['Time Series (Daily)'].hasOwnProperty(key)) {
                        console.log('____________________________________________________');
                        console.log(asset.name);
                        console.log(data['Meta Data']['2. Symbol']);
                        console.log(data['Time Series (Daily)'][key]['4. close']);
                        console.log(key);
                        console.log('____________________________________________________');
                        firebase_1.fb.firestore().collection(`/users/${userId}/markets/${marketId}/assets/${asset.assetId}/series`).doc(key).set({
                            'name': asset.name,
                            'symbol': data['Meta Data']['2. Symbol'],
                            'close': data['Time Series (Daily)'][key]['4. close'],
                            'date': key,
                        });
                    }
                }
            });
        });
    }
    fetchAsset(userId, marketId, assetId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield firebase_1.fb.firestore().doc(`/users/${userId}/markets/${marketId}/assets/${assetId}`).get().then(asset => {
                this.asset = new asset_model_1.Asset(asset.data().assetId, asset.data().name, asset.data().symbol);
            });
        });
    }
    fetchAssets(userId, marketId) {
        return __awaiter(this, void 0, void 0, function* () {
            this.assets = [];
            yield firebase_1.fb.firestore().collection(`/users/${userId}/markets/${marketId}/assets`).get().then(assets => {
                assets.forEach(asset => {
                    this.assets.push(new asset_model_1.Asset(asset.data().assetId, asset.data().name, asset.data().symbol));
                });
            });
        });
    }
    /////////////
    // Getters //
    /////////////
    getAsset(userId, marketId, assetId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.fetchAsset(userId, marketId, assetId);
            return new Promise(resolve => resolve(this.asset));
        });
    }
    getAssets(userId, marketId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.fetchAssets(userId, marketId);
            return new Promise(resolve => resolve(this.assets));
        });
    }
    /////////////
    // Setters //
    /////////////
    setAsset(asset) {
        this.asset = asset;
    }
    setAssets(assets) {
        this.assets = assets;
    }
}
exports.AssetService = AssetService;
//# sourceMappingURL=asset-service.js.map