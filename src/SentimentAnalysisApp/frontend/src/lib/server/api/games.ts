import type { Game } from '../../shared/types';

export async function getGames(): Promise<Array<Game>> {
	const response = await fetch('http://127.0.0.1:8000/games/', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (!response.ok) {
		if (response.status === 401) {
			throw new Error('Unauthorized access. Please provide a valid JWT token.');
		} else if (response.status === 404) {
			throw new Error('Resource not found. Please check the API endpoint URL.');
		} else {
			throw new Error(`Unexpected response. Response status: ${response.status}`);
		}
	}

	return await response.json();
}

export async function getGame(gameId: string): Promise<Game> {
	const response = await fetch(`http://127.0.0.1:8000/games/${gameId}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (!response.ok) {
		if (response.status === 401) {
			throw new Error('Unauthorized access. Please provide a valid JWT token.');
		} else if (response.status === 404) {
			throw new Error('Resource not found. Please check the API endpoint URL.');
		} else {
			throw new Error(`Unexpected response. Response status: ${response.status}`);
		}
	}

	return await response.json();
}
