const move_cam_dir_2_code = {
    right: 4,
    left: 3,
}
const move_cam_servo = (dir) => ({
    N: 106,
    D1: move_cam_dir_2_code[dir]
})

const set_cam_servo = (angle) => ({
    N: 5,
    D1: 1,
    D2: angle
})



const get_ultra_value = () => ({
    N: 21,
    D1: 2 
})


const rocker_move_dir_2_code = {
    forward: 1,
    backward: 2,
    left: 3,
    right: 4,
    leftForward: 5,
    leftBackward: 6,
    rightForward: 7,
    rightBackward: 8,
    stop: 9,
}
const rocker_move = (dir, speed) => ({
    N: 102,
    D1: rocker_move_dir_2_code[dir],
    D2: speed
})


export {
    move_cam_servo,
    set_cam_servo,
    rocker_move,
    get_ultra_value
}