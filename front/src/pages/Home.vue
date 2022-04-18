<script setup lang="ts">
import { ref } from "vue"
import type { UploadProps } from "element-plus"
import { toGray,binarize } from "@/services/FileUpload"

type Image = {
    task_id: string
    id: string
    url: string
    gray_id?: string
    gray_url?: string
    binarized_id?:string
    binarized_url?:string
    threshold?:number
}

const images = ref<Image[]>([])

const loading = ref<boolean>(false)


const uploadAPIUrl = `${import.meta.env.VITE_API_URL}/upload_image`

const handleRemove: UploadProps["onRemove"] = (file, uploadFiles) => {
    console.log(file, uploadFiles)
}

const handleUploadSuccess: UploadProps["onSuccess"] = (response) => {
    const task_id = response.result.image.task_id
    const id = response.result.image.id
    const image = {
        task_id: task_id,
        id: id,
        url: `${import.meta.env.VITE_API_URL}/static/task/${task_id}/${id}.jpg`,
        gray_id: "",
        gray_url: "",
        threshold: 0
    }
    images.value.push(image)
}

const handleGrayScale = async (id: string) => {
    let image = images.value.find((v) => v.id === id)
    if (image) {
        loading.value = true
        try {
            const res = await toGray(image)
            image.gray_id = res.result.image.id
            image.gray_url = `${import.meta.env.VITE_API_URL}/static/task/${
                res.result.image.task_id
            }/${res.result.image.id}.jpg`
        } catch (e) {
            console.log(e)
        } finally {
            loading.value = false
        }
    }
}

const handleBinarize = async (id: string) => {
    let image = images.value.find((v) => v.id === id)
    if (image) {
        loading.value = true
        try {
            const res = await binarize(image)
            image.binarized_id = res.result.image.id
            image.binarized_url = `${import.meta.env.VITE_API_URL}/static/task/${
                res.result.image.task_id
            }/${res.result.image.id}.jpg`
            
            if(image.threshold === 0){
                image.threshold = res.result.params.threshold
            }
        } catch (e) {
            console.log(e)
        } finally {
            loading.value = false
        }
    }
}

const grayImageExists = (id: string) => {
    const image = images.value.find((v) => v.id === id && v.gray_url !== "")
    if (image) {
        return true
    } else {
        return false
    }
}
</script>

<template>
    <el-upload
        :action="uploadAPIUrl"
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
                            v-if="!grayImageExists(image.id)"
                            class="button"
                            type="text"
                            v-loading="loading"
                            @click="handleGrayScale(image.id)"
                            >グレースケール</el-button
                        >
                        <el-form
                            v-if="grayImageExists(image.id)"
                            :inline="true"
                        >
                            <el-form-item label="閾値">
                                <el-input-number
                                    v-model="image.threshold"
                                    :min="0"
                                    :max="255"
                                />
                            </el-form-item>
                            <el-form-item>
                                <el-button
                                    type="primary"
                                    @click="handleBinarize(image.id)"
                                    >二値化する</el-button
                                >
                            </el-form-item>
                        </el-form>
                    </div>
                </template>
                <img :src="image.url" class="image" />
                <img
                    v-if="image.gray_url"
                    :src="image.gray_url"
                    class="image"
                />
                <img
                    v-if="image.binarized_url"
                    :src="image.binarized_url"
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
    padding: 20px 0;
}
</style>
