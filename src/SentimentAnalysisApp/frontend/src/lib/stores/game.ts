import { browser } from '$app/environment';
import { writable } from 'svelte/store';
import type {Game, User} from "../shared/types";

const makeInitialValue = () => {
    return [] as Game[];
}
const gameStore = writable<Game[]>(makeInitialValue());
const gameFilter = writable<Record<string, any>>({source: 'all'});
const gameSort = writable<string>('');
gameStore.subscribe((value) => {

 });

 export default gameStore;