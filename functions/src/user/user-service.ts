import { fb } from '../config/firebase'
import { User } from './user-model'


export class UserService {

	///////////////
	// Variables //
	///////////////
	private user: User
	private users: User[]

	///////////////
	// Functions //
	///////////////
	public async fetchUsers(): Promise<void> {
	
		await fb.firestore().collection(`/users`).get().then(users => {
	
			users.forEach(user => this.users.push( new User(user.data().userId) ))
	
		})
	
	}

	public async fetchUser(userId: string): Promise<void> {
	
		await fb.firestore().doc(`/users/${userId}`).get().then(user => {
			
			this.user = new User(user.data().userId)
		
		})
		
	}

	/////////////
	// Getters //
	/////////////
	
	public async getUser(userId: string): Promise<User> {

		await this.fetchUser(userId)
		return new Promise<User>(resolve => resolve(this.user))

	}


	public async getUsers(): Promise<User[]> {
		
		await this.fetchUsers()
		return new Promise<User[]>(resolve => resolve(this.users))
	
	}

	/////////////
	// Setters //
	/////////////
	public setUser(user: User): void {
	
		this.user = user
	
	}

	public setUsers(users: User[]): void {
	
		this.users = users
	
	}


}