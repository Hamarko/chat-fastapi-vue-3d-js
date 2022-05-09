<template>
  <marker 
    :id="id"
    markerWidth="10" 
    markerHeight="10" 
    refX="15" 
    refY="0" 
    orient="auto" 
    markerUnits="strokeWidth" 
    viewBox="0 -5 10 10"
  >
    <path d="M0,-5L10,0L0,5"></path>
  </marker>
</template>

<script>
export default {
  name: 'D3MarkerArrow',
  props: ["id"]
}
</script>

<style>

</style>