<script setup lang="ts">
import { ref } from "vue"
import { ElMessageBox } from "element-plus"
import type { UploadProps, UploadUserFile } from "element-plus"

const fileList = ref<UploadUserFile[]>([])
const dialogVisible = ref(false)
const dialogImageUrl = ref("")

const handleRemove: UploadProps["onRemove"] = (file, uploadFiles) => {
    console.log(file, uploadFiles)
}

const handlePreview: UploadProps["onPreview"] = (uploadFile) => {
    dialogImageUrl.value =
        "http://localhost:5010/static/task/" +
        uploadFile.response.result.image.task_id +
        "/" +
        uploadFile.response.result.image.id + 
        ".jpg"
    dialogVisible.value = true
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
        :file-list="fileList"
        name="uploadFile"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        multiple
    >
        <el-button type="primary">アップロード</el-button>
        <template #tip>
            <div class="el-upload__tip">
                jpg/png files with a size less than 500KB.
            </div>
        </template>
    </el-upload>
    <el-dialog v-model="dialogVisible">
        <img w-full :src="dialogImageUrl" alt="Preview Image" />
    </el-dialog>
</template>
