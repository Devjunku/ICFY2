<template>
  <div class="mb-1">{{ person.username }}</div>
</template>

<script>
export default {
  name: 'FollowItem',
  props: {
    person: {
      type: Object
    }
  },
}
</script>

<style>

</style>