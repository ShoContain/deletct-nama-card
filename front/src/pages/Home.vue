<script setup lang="ts">
import { ref } from "vue"
import type { UploadProps } from "element-plus"
import { toGray } from "@/services/FileUpload"

type Image = {
    task_id: string
    id: string
    url: string
    gray_id?: string
    gray_url?: string
}

const images = ref<Image[]>([])

const loading = ref<boolean>(false)

const handleRemove: UploadProps["onRemove"] = (file, uploadFiles) => {
    console.log(file, uploadFiles)
}

const handleUploadSuccess: UploadProps["onSuccess"] = (response) => {
    const task_id = response.result.image.task_id
    const id = response.result.image.id
    const image = {
        task_id: task_id,
        id: id,
        url: `http://localhost:5010/static/task/${task_id}/${id}.jpg`,
    }
    images.value.push(image)
}

const grayScale = async (id: string) => {
    let image = images.value.find((v) => v.id === id)
    loading.value = true
    try {
        const res = await toGray(image)
        const gray_id = res.result.image.id
        const task_id = res.result.image.task_id
        if (gray_id && task_id) {
            image.gray_id = gray_id
            image.gray_url = `http://localhost:5010/static/task/${task_id}/${gray_id}.jpg`
        }
    } catch (e) {
        console.log(e)
    } finally {
        loading.value = false
    }
}

const grayImageExists = (id: string) => {
    const image = images.value.find((v) => v.id === id)
    if ( 'gray_url' in image  && image.gray_url !== null) {
        return true
    } else {
        return false
    }
}
</script>

<template>
    <el-upload
        action="http://localhost:5010/upload_image"
        name="uploadFile"
        :on-remove="handleRemove"
        :on-success="handleUploadSuccess"
        multiple
    >
        <el-button type="primary">アップロード</el-button>
        <template #tip>
            <div class="el-upload__tip">
                jpg/png files with a size less than 500KB.
            </div>
        </template>
    </el-upload>
    <el-row v-if="images.length > 0">
        <el-col v-for="(image, index) in images" :key="index" :span="8">
            <el-card>
                <template #header>
                    <div class="card-header">
                        <el-button
                            class="button"
                            type="text"
                            v-loading="loading"
                            :disabled="grayImageExists(image.id)"
                            @click="grayScale(image.id)"
                            >グレースケール</el-button
                        >
                    </div>
                </template>
                <img :src="image.url" class="image" />
                <img
                    v-if="grayImageExists(image.id)"
                    :src="image.gray_url"
                    class="image"
                />
            </el-card>
        </el-col>
    </el-row>
</template>
<style scoped>
.image {
    width: 100%;
    display: block;
    margin:20px 
}
</style>
