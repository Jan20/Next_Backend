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
const user_model_1 = require("./user-model");
class UserService {
    ///////////////
    // Functions //
    ///////////////
    fetchUsers() {
        return __awaiter(this, void 0, void 0, function* () {
            yield firebase_1.fb.firestore().collection(`/users`).get().then(users => {
                users.forEach(user => this.users.push(new user_model_1.User(user.data().userId)));
            });
        });
    }
    fetchUser(userId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield firebase_1.fb.firestore().doc(`/users/${userId}`).get().then(user => {
                this.user = new user_model_1.User(user.data().userId);
            });
        });
    }
    /////////////
    // Getters //
    /////////////
    getUser(userId) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.fetchUser(userId);
            return new Promise(resolve => resolve(this.user));
        });
    }
    getUsers() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.fetchUsers();
            return new Promise(resolve => resolve(this.users));
        });
    }
    /////////////
    // Setters //
    /////////////
    setUser(user) {
        this.user = user;
    }
    setUsers(users) {
        this.users = users;
    }
}
exports.UserService = UserService;
//# sourceMappingURL=user-service.js.map