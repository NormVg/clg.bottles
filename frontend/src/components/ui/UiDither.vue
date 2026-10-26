<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  ShaderMount,
  getShaderColorFromString,
  ShaderFitOptions,
  defaultObjectSizing,
} from '@paper-design/shaders'
import { DitheringShapes, DitheringTypes, ditheringFragmentShader } from './ditheringShader'

const props = withDefaults(
  defineProps<{
    colorBack?: string
    colorFront?: string
    shape?: keyof typeof DitheringShapes
    type?: keyof typeof DitheringTypes
    size?: number
    speed?: number
    frame?: number
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
    colorBack: '#000000',
    colorFront: '#FFFFFF',
    shape: 'simplex',
    type: '4x4',
    size: 2,
    speed: 1,
    frame: 0,
    fit: defaultObjectSizing.fit,
    scale: 1,
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
let shader: ShaderMount | null = null
let destroyed = false

function uniforms() {
  return {
    u_colorBack: getShaderColorFromString(props.colorBack),
    u_colorFront: getShaderColorFromString(props.colorFront),
    u_shape: DitheringShapes[props.shape] ?? 1,
    u_type: DitheringTypes[props.type] ?? 3,
    u_pxSize: props.size,
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

function update() {
  if (destroyed) return
  try {
    if (shader) {
      shader.setUniforms(uniforms())
    } else if (container.value) {
      shader = new ShaderMount(
        container.value,
        ditheringFragmentShader,
        uniforms(),
        { alpha: true, premultipliedAlpha: false, antialias: false },
        props.speed,
        props.frame,
        props.minPixelRatio,
        props.maxPixelCount,
      )
    }
  } catch (error) {
    console.error('dithering shader failed', error)
  }
}

onMounted(update)

watch(
  () => [
    props.colorBack,
    props.colorFront,
    props.shape,
    props.type,
    props.size,
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
})
</script>

<template>
  <div ref="container" class="paper-shader-container"></div>
</template>

<style scoped>
.paper-shader-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.paper-shader-container :deep(canvas) {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
