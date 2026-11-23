<script setup lang="ts">
interface Props {
  modelValue: string
  label: string
  name: string
  type?: 'text' | 'tel' | 'number' | 'textarea'
  placeholder?: string
  required?: boolean
  minlength?: number
  maxlength?: number
  min?: number
  step?: number
  rows?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  required: false,
  rows: 4,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const update = (event: Event) => {
  const element = event.target as HTMLInputElement | HTMLTextAreaElement
  emit('update:modelValue', element.value)
}

const inputClass =
  'w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:placeholder:text-slate-600 dark:focus:border-blue-400'
</script>

<template>
  <label class="block">
    <span class="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">
      {{ label }}
      <span v-if="required" class="text-rose-500">*</span>
    </span>
    <textarea
      v-if="props.type === 'textarea'"
      :id="name"
      :name="name"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :minlength="minlength"
      :maxlength="maxlength"
      :rows="rows"
      :class="inputClass"
      @input="update"
    />
    <input
      v-else
      :id="name"
      :name="name"
      :type="props.type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :minlength="minlength"
      :maxlength="maxlength"
      :min="min"
      :step="step"
      :class="inputClass"
      @input="update"
    />
  </label>
</template>
