import {z} from "zod";
export type validationResultType = {success: boolean, errors: Record<string, any>}
export function validateFormData<T>(data: T, schema: z.ZodSchema<T>): validationResultType{
    try {
        schema.parse(data);
        return {
            success: true,
            errors: {}
        }
    } catch (err) {
        if (err instanceof z.ZodError) {
            const {fieldErrors: errors} = err.flatten();
            return {
                success: false,
                errors
            };
        }
        return {
            success: false,
            errors: {}
        }
    }
}