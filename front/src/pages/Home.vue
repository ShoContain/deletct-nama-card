<script setup lang="ts">
import { ref } from "vue"
import type { UploadProps } from "element-plus"
import { toGray, binarize } from "@/services/FileUpload"

type Image = {
    task_id: string
    id: string
    url: string
    gray_id?: string
    gray_url?: string
    binarized_id?: string
    binarized_url?: string
    threshold?: number
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
        threshold: 0,
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
            image.binarized_url = `${
                import.meta.env.VITE_API_URL
            }/static/task/${res.result.image.task_id}/${
                res.result.image.id
            }.jpg`

            if (image.threshold === 0) {
                image.threshold = res.result.params.threshold
            }
        } catch (e) {
            console.log(e)
        } finally {
            loading.value = false
        }
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
        <el-col v-for="(image, index) in images" :key="index" :span="24">
            <el-card>
                <template #header>
                    <div class="card-header">
                        <el-form size="small">
                            <el-form-item label="グレースケール">
                                <el-button
                                    type="primary"
                                    @click="handleGrayScale(image.id)"
                                    >実行</el-button
                                >
                            </el-form-item>
                            <el-form-item label="二値化(閾値を設定できます)">
                                <el-input-number
                                    v-model="image.threshold"
                                    :min="0"
                                    :max="255"
                                    placeholder="閾値を設定してください"
                                    label="閾値"
                                />
                                <el-button
                                    type="primary"
                                    @click="handleBinarize(image.id)"
                                    >実行</el-button
                                >
                            </el-form-item>
                        </el-form>
                    </div>
                </template>
                <img v-if="image.url" :src="image.url" class="image" />
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
.el-button--small {
    margin: 0 20px;
}
.image {
    display: inline-block;
    margin: 0 20px;
    width: 200px;
}
</style>
