import { writable } from 'svelte/store';

interface Character {
    id: number;
    name: string;
    planet_name: string;
    image_url: string;
}

interface CharacterState {
    thread_id: number;
    character: Character;
}

export const characterStore = writable<CharacterState | null>(null);