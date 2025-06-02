import { browser } from '$app/environment';
// TODO: Why not user $state/$effect runes?
import { writable } from 'svelte/store';

interface Character {
  id: number;
  name: string;
  planet_name: string;
  image_url: string;
}

interface CharacterState {
  thread_id: number;
  conversation_id: string;
  character: Character;
}

const initialValue: CharacterState | null =
  browser ? JSON.parse(localStorage.getItem('characterState') || 'null') : null;

export const characterStore = writable<CharacterState | null>(initialValue);

if (browser) {
  characterStore.subscribe((value) => {
    localStorage.setItem('characterState', JSON.stringify(value));
  });
}
