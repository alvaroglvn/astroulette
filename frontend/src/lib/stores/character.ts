import { browser } from '$app/environment';
import { writable, type Writable } from 'svelte/store';

interface Character {
  id: number;
  name: string;
  planet_name: string;
  image_url: string;
}

type CharacterState = {
  thread_id: number;
  conversation_id: string;
  character: Character;
};

export const characterState: Writable<CharacterState | null> = writable(
  browser ? JSON.parse(localStorage.getItem('characterState') || 'null') : null,
);

if (browser) {
  characterState.subscribe((value) => {
    localStorage.setItem('characterState', JSON.stringify(value));
  });
}
