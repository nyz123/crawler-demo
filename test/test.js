async function test(){
    try {
        await new Promise(function (resolve,reject) {
            reject('xdl')
        })
    } catch (e) {
        console.log(22);
    }
}
test()