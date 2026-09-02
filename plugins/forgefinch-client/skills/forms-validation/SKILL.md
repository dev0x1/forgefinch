---
name: forms-validation
description: "Use for React Hook Form, Zod form schemas, field errors, async submit flows, dirty-state prompts, settings forms, create/edit dialogs, and form tests."
---

# forms-validation

Before applying this guidance, read `AGENTS.md` and inspect the existing project structure, package manager, scripts, and tests. Treat example paths as responsibility labels and map them to repository-owned equivalents; do not create a suggested layout unless the task requires it.

## Purpose

Build forms with one source of truth: Zod schema for data shape, React Hook Form for in-progress form state, and explicit submit/cancel behavior.

## Use this skill when

- adding create/edit/settings forms, dialogs, validation schemas, submit flows, dirty-state warnings, async save behavior, or form tests
- fixing validation bugs, inaccessible fields, broken reset behavior, or duplicate form state

## Non-negotiable rules

- Every form has a Zod schema.
- Form value types are inferred from the Zod schema.
- React Hook Form owns in-progress field state. Do not duplicate form values in Zustand or component state.
- Submit buttons show pending state and prevent duplicate submit.
- Every field error is visible and programmatically associated with its field.
- Every form has tests for valid submit, invalid submit, and cancel/reset behavior.

## Required workflow

1. Write the schema and default values first.
2. Build the form with accessible labels, descriptions, and error messages.
3. Connect submit to a typed mutation or preload API through feature hooks.
4. Add tests for invalid and valid flows before final styling.
5. Verify keyboard navigation, dirty state, pending state, and error display.

## Repo placement

- Feature forms live under `<desktop-app-root>/src/renderer/src/features/<feature>`.
- Reusable form UI lives under `<desktop-app-root>/src/renderer/src/components`.
- IPC-crossing form schemas live in `<desktop-app-root>/src/shared/schemas`; purely visual schemas can live beside the feature form.
- Submit hooks that call preload APIs live at the feature boundary, not inside presentational inputs.
- Component tests live beside forms; app-level dirty-state or navigation prompts belong in `<desktop-app-root>/tests/e2e` when user flow matters.

## Patterns And Examples

- Schema: define user-readable messages, infer form values with `z.infer`, normalize trimming/defaults explicitly, and reuse shared schemas only when UI and IPC boundary rules are identical.
- Component: initialize `useForm` with `zodResolver`, semantic form controls, accessible labels, explicit cancel/reset, and no duplicate form state.
- Field errors: render one message per invalid field, connect it with `aria-describedby`, set `aria-invalid`, and avoid technical schema paths in copy.
- Async submit: use a typed feature hook or TanStack Query mutation, disable submit while pending, prevent duplicate submit, map known errors to field/form messages, and invalidate affected queries on success.
- Dirty state: prompt only when dirty and not successfully submitted; reset dirty state after save or explicit discard.
- Settings: load settings through a typed query, save through validated IPC, and provide restore defaults behavior.

Form example:

```tsx
const formSchema = z.object({
  title: z.string().trim().min(1, 'Title is required.')
})

type FormValues = z.infer<typeof formSchema>

export function ExampleForm({ onSubmit }: { readonly onSubmit: (values: FormValues) => Promise<void> }) {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { title: '' }
  })

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} noValidate>
      <label htmlFor="example-title">Title</label>
      <input id="example-title" aria-invalid={Boolean(form.formState.errors.title)} {...form.register('title')} />
      {form.formState.errors.title ? <p role="alert">{form.formState.errors.title.message}</p> : null}
      <button type="submit" disabled={form.formState.isSubmitting}>Save</button>
    </form>
  )
}
```

## Required checks

- `pnpm typecheck`
- `pnpm lint`
- `pnpm test`

## Completion report additions

Include the exact skill name `forms-validation`, changed files, commands run, tests added or changed, manual verification, and residual risk. Do not report a check as passed unless it actually ran and passed.
