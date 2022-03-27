<script setup lang="ts">
import { ref } from "vue"
import { ElMessageBox } from "element-plus"
import type { UploadProps, UploadUserFile } from "element-plus"

const fileList = ref<UploadUserFile[]>([
    {
        name: "food.jpeg",
        url: "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100",
    },
    {
        name: "food2.jpeg",
        url: "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100",
    },
])

const handleRemove: UploadProps["onRemove"] = (file, uploadFiles) => {
    console.log(file, uploadFiles)
}

const handlePreview: UploadProps["onPreview"] = (uploadFile) => {
    console.log(uploadFile)
}

const beforeRemove: UploadProps["beforeRemove"] = (uploadFile, uploadFiles) => {
    return ElMessageBox.confirm(
        `Cancel the transfert of ${uploadFile.name} ?`
    ).then(
        () => true,
        () => false
    )
}
</script>

<template>
    <el-upload
        action="http://localhost:5010/upload_image"
        name="uploadFile"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        multiple
        :file-list="fileList"
    >
        <el-button type="primary">アップロード</el-button>
        <template #tip>
            <div class="el-upload__tip">
                jpg/png files with a size less than 500KB.
            </div>
        </template>
    </el-upload>
</template>
