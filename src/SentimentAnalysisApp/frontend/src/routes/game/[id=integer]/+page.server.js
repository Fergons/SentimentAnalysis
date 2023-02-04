import {error} from '@sveltejs/kit';

// @ts-ignore
export async function load({params}) {
    const games = [
        {
            id: 1,
            name: 'Rainbow Six Siege',
            description: 'Svelte Material UI is a library of Svelte components that implement Google\'s Material Design specification.',
            image: 'https://raw.githubusercontent.com/hperrin/svelte-material-ui/master/packages/site/src/images/smui-logo.png',
            link: ''
        },
        {
            id: 2,
            name: 'Svelte Material UI',
            description: 'Svelte Material UI is a library of Svelte components that implement Google\'s Material Design specification.',
            image: 'https://raw.githubusercontent.com/hperrin/svelte-material-ui/master/packages/site/src/images/smui-logo.png',
            link: ''
        }
    ];

    let game = games.find(game => game.id === parseInt(params.id));
    // console.log(params.id);
    // console.log(game);
    if (game){
        return {
            title: game.name + " | Overview",
            game: game
        }
    }

    throw error(404, 'Not found');
}