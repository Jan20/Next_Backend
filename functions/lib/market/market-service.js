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
const market_model_1 = require("./market-model");
class MarketService {
    ///////////////
    // Functions //
    ///////////////
    fetchMarkets(userId) {
        return __awaiter(this, void 0, void 0, function* () {
            this.markets = [];
            yield firebase_1.fb.firestore().collection(`/users/${userId}/markets`).get().then(markets => {
                markets.forEach(market => this.markets.push(new market_model_1.Market(market.data().marketId)));
            });
        });
    }
    fetchMarket(userId, marketId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield firebase_1.fb.firestore().doc(`/users/${userId}/markets/${marketId}`).get().then(market => {
                this.market = new market_model_1.Market(market.data().marketId);
            });
        });
    }
    /////////////
    // Getters //
    /////////////
    getMarket(userId, marketId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.fetchMarket(userId, marketId);
            return new Promise(resolve => resolve(this.market));
        });
    }
    getMarkets(userId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.fetchMarkets(userId);
            return new Promise(resolve => resolve(this.markets));
        });
    }
    /////////////
    // Setters //
    /////////////
    setMarket(market) {
        this.market = market;
    }
    setMarkets(markets) {
        this.markets = markets;
    }
}
exports.MarketService = MarketService;
//# sourceMappingURL=market-service.js.map