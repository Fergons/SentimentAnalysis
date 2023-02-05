export type Game = {
	id: number;
	updated_at: string;
	name: string;
	image_url: string;
	release_date: string;
};

export type User = {
	id: string;
	email: string;
	is_active: boolean;
	is_superuser: boolean;
	is_verified: boolean;
};
