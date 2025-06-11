import { browser } from '$app/environment';


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


export let $characterState = $state<CharacterState | null>(
  browser ? JSON.parse(localStorage.getItem('characterState') || 'null') : null
);

if (browser) {
  $effect(() => {
    localStorage.setItem('characterState', JSON.stringify($characterState));
  });
}
