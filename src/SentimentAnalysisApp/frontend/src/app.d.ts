// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
    namespace App {
        // interface Error {}
        interface Locals {
            token?: string;
            user?: {
                id?: string;
                email: string;
                is_active?: boolean;
				is_superuser?: boolean;
				is_verified?: boolean;
            }
        }

        // interface PageData {}
        // interface Platform {}
    }
}

export {};
