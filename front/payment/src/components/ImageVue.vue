<template>
  <v-img v-if="imageUrl" :src="imageUrl"></v-img>
</template>

<script setup>
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3'
import { ref, onMounted } from 'vue'

const props = defineProps({
  imgSrc: String,
})

const url = props.imgSrc
const parsedUrl = new URL(url)
const path = parsedUrl.pathname.slice(1)

const imageUrl = ref(null)
const bucketName = 'demo-bucket-1222'
const objectKey = path

const fetchImageFromS3 = async () => {
  const client = new S3Client({
    region: 'ap-northeast-2',
    credentials: {
      accessKeyId: import.meta.env.VITE_APP_S3_ACCESS_KEY_ID,
      secretAccessKey: import.meta.env.VITE_APP_S3_SECRET_ACCESS_KEY,
    },
  })

  const command = new GetObjectCommand({
    Bucket: bucketName,
    Key: objectKey,
  })

  try {
    const response = await client.send(command)

    const reader = response.Body.getReader()
    const streamToArrayBuffer = async (reader) => {
      const chunks = []
      let done = false

      while (!done) {
        const { value, done: doneReading } = await reader.read()
        if (value) {
          chunks.push(value)
        }
        done = doneReading
      }

      const length = chunks.reduce((acc, chunk) => acc + chunk.length, 0)
      const arrayBuffer = new Uint8Array(length)
      let offset = 0

      for (const chunk of chunks) {
        arrayBuffer.set(chunk, offset)
        offset += chunk.length
      }

      return arrayBuffer.buffer
    }

    const arrayBuffer = await streamToArrayBuffer(reader)
    const blob = new Blob([arrayBuffer], { type: response.ContentType })
    imageUrl.value = URL.createObjectURL(blob)
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  fetchImageFromS3()
})
</script>