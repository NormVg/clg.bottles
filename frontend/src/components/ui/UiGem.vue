<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  ShaderMount,
  gemSmokeFragmentShader,
  getShaderColorFromString,
  GemSmokeShapes,
  ShaderFitOptions,
  defaultObjectSizing,
} from '@paper-design/shaders'
import { processGemImage } from './gemImage'

const props = withDefaults(
  defineProps<{
    colors?: string[]
    colorBack?: string
    colorInner?: string
    image?: string
    speed?: number
    frame?: number
    innerDistortion?: number
    outerDistortion?: number
    outerGlow?: number
    innerGlow?: number
    offset?: number
    angle?: number
    size?: number
    shape?: keyof typeof GemSmokeShapes
    fit?: keyof typeof ShaderFitOptions
    scale?: number
    rotation?: number
    originX?: number
    originY?: number
    offsetX?: number
    offsetY?: number
    worldWidth?: number
    worldHeight?: number
    minPixelRatio?: number
    maxPixelCount?: number
  }>(),
  {
    colors: () => ['#333333', '#e7e6df'],
    colorBack: '#f0efea',
    colorInner: '#fafaf5',
    image: '',
    speed: 1,
    frame: 0,
    innerDistortion: 0.8,
    outerDistortion: 0.6,
    outerGlow: 0.55,
    innerGlow: 1,
    offset: 0,
    angle: 0,
    size: 0.8,
    shape: 'diamond',
    fit: defaultObjectSizing.fit,
    scale: 0.6,
    rotation: defaultObjectSizing.rotation,
    originX: defaultObjectSizing.originX,
    originY: defaultObjectSizing.originY,
    offsetX: defaultObjectSizing.offsetX,
    offsetY: defaultObjectSizing.offsetY,
    worldWidth: defaultObjectSizing.worldWidth,
    worldHeight: defaultObjectSizing.worldHeight,
    minPixelRatio: 2,
    maxPixelCount: 1920 * 1080 * 4,
  },
)

const container = ref<HTMLElement | null>(null)
const ready = ref(false)
let shader: ShaderMount | null = null
let currentObjectUrl: string | null = null
let destroyed = false

async function uniforms() {
  const result = await processGemImage(props.image)
  if (currentObjectUrl) URL.revokeObjectURL(currentObjectUrl)
  currentObjectUrl = result.objectUrl
  if (destroyed) throw new Error('destroyed')

  return {
    u_colors: props.colors.map(getShaderColorFromString),
    u_colorsCount: props.colors.length,
    u_colorBack: getShaderColorFromString(props.colorBack),
    u_image: result.image,
    u_innerDistortion: props.innerDistortion,
    u_outerDistortion: props.outerDistortion,
    u_outerGlow: props.outerGlow,
    u_innerGlow: props.innerGlow,
    u_colorInner: getShaderColorFromString(props.colorInner),
    u_offset: props.offset,
    u_angle: props.angle,
    u_size: props.size,
    u_isImage: Boolean(props.image),
    u_shape: GemSmokeShapes[props.shape],
    u_fit: ShaderFitOptions[props.fit],
    u_scale: props.scale,
    u_rotation: props.rotation,
    u_offsetX: props.offsetX,
    u_offsetY: props.offsetY,
    u_originX: props.originX,
    u_originY: props.originY,
    u_worldWidth: props.worldWidth,
    u_worldHeight: props.worldHeight,
  }
}

async function update() {
  if (destroyed) return
  try {
    const values = await uniforms()
    if (destroyed) return

    if (shader) {
      shader.setUniforms(values)
    } else if (container.value) {
      shader = new ShaderMount(
        container.value,
        gemSmokeFragmentShader,
        values,
        { alpha: true, premultipliedAlpha: false, antialias: false },
        props.speed,
        props.frame,
        props.minPixelRatio,
        props.maxPixelCount,
        ['u_image'],
      )
    }

    requestAnimationFrame(() => {
      ready.value = true
    })
  } catch (error) {
    console.error('gem shader failed', error)
  }
}

onMounted(update)

watch(
  () => [
    props.colors,
    props.colorBack,
    props.colorInner,
    props.image,
    props.innerDistortion,
    props.outerDistortion,
    props.outerGlow,
    props.innerGlow,
    props.offset,
    props.angle,
    props.size,
    props.shape,
    props.fit,
    props.scale,
    props.rotation,
    props.originX,
    props.originY,
    props.offsetX,
    props.offsetY,
    props.worldWidth,
    props.worldHeight,
  ],
  update,
  { deep: true },
)

watch(() => props.speed, (value) => shader?.setSpeed(value))
watch(() => props.frame, (value) => shader?.setFrame(value))

onBeforeUnmount(() => {
  destroyed = true
  shader?.dispose()
  shader = null
  if (currentObjectUrl) URL.revokeObjectURL(currentObjectUrl)
})
</script>

<template>
  <div ref="container" class="gem" :class="{ 'gem--ready': ready }"></div>
</template>

<style scoped>
.gem {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: scale(0.95);
  transition: opacity 1s var(--ease-out), transform 1s var(--ease-out);
}

.gem--ready {
  opacity: 1;
  transform: scale(1);
}

.gem :deep(canvas) {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
