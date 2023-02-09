export type TextfieldInputState = {
    value: string | null,
    dirty: boolean,
    invalid: boolean,
    focused: boolean,
    helperText: string
};

export function makeDefaultTextfieldInputState(value: string | null = null,
                                               dirty: boolean = true,
                                               invalid: boolean = false,
                                               focused: boolean = false): TextfieldInputState {
    return {
        value: value ?? null,
        dirty: dirty,
        invalid: invalid,
        focused: focused,
        helperText: '',
    };
}

export function isTextfieldInputStateValid(state: TextfieldInputState): boolean {
    return state.value !== null && state.dirty && !state.invalid && !state.focused;
}