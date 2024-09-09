-- 주차 구역 데이터 삽입
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('S1', FALSE, FALSE, 6, 0, '경차');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('S2', FALSE, FALSE, 6, 1, '경차');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('S3', FALSE, FALSE, 6, 2, '경차');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('S4', FALSE, FALSE, 6, 3, '경차');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('E1', TRUE, TRUE, 6, 4, '전기차'); -- 점유 상태 (브라우니)
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('E2', FALSE, FALSE, 6, 5, '전기차');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('A1', FALSE, FALSE, 4, 2, '일반');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('A2', FALSE, TRUE, 4, 3, '일반'); -- 주차 금지 구역
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('A3', FALSE, FALSE, 4, 4, '장애인');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('B1', TRUE, TRUE, 3, 2, '일반'); -- 점유 상태 (차량 with 초음파 압력)
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('B2', TRUE, TRUE, 3, 3, '일반'); -- 점유 상태 (후렌치 파이)
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('B3', FALSE, FALSE, 3, 4, '장애인');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('C1', FALSE, FALSE, 1, 2, '일반');
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('C2', TRUE, TRUE, 1, 3, '일반'); -- 점유 상태 (카스타드)
INSERT INTO ParkingSpot (code, isOccupied, isHere, x, y, type) VALUES ('C3', FALSE, FALSE, 1, 4, '여성전용');

-- 기타 차량 데이터 삽입
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('123가4567', '일반', '2024-08-16 08:05:00', '2024-08-16 09:00:00', 3000, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('345다6789', '경차', '2024-08-16 08:25:00', '2024-08-16 09:20:00', 3000, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('234나5678', '일반', '2024-08-16 08:15:00', '2024-08-16 09:25:00', 3500, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('890아1534', '경차', '2024-08-16 08:15:00', '2024-08-16 09:30:00', 4000, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('789사0123', '전기차', '2024-08-16 08:05:00', '2024-08-16 09:40:00', 5000, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('234타5678', '경차', '2024-08-16 08:55:00', '2024-08-16 09:40:00', 2500, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('345파6789', '일반', '2024-08-16 08:05:00', '2024-08-16 09:50:00', 5500, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('567가8901', '전기차', '2024-08-16 08:25:00', '2024-08-16 09:50:00', 4500, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('456라7890', '경차', '2024-08-16 08:35:00', '2024-08-16 10:00:00', 4500, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('39카4567', '경차', '2024-08-16 08:45:00', '2024-08-16 10:00:00', 4000, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('567마8901', '일반', '2024-08-16 08:45:00', '2024-08-16 10:00:00', 4000, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('46하7890', '일반', '2024-08-16 08:15:00', '2024-08-16 10:10:00', 6000, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('901자2345', '일반', '2024-08-16 08:25:00', '2024-08-16 10:10:00', 5500, NULL, NULL);
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('12차3456', '일반', '2024-08-16 08:35:00', '2024-08-16 10:20:00', 5500, NULL, NULL);

-- 차량 데이터 삽입 (점유된 상태)
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('94조9259', '전기차', '2024-08-16 08:00:00', NULL, NULL, 'https://demo-bucket-1222.s3.ap-northeast-2.amazonaws.com/images/ev1.jpg', (SELECT id FROM ParkingSpot WHERE code = 'E1'));
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('15로5301', '일반', '2024-08-16 08:30:00', NULL, NULL, 'https://demo-bucket-1222.s3.ap-northeast-2.amazonaws.com/images/b1.jpg', (SELECT id FROM ParkingSpot WHERE code = 'B1'));
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('32모5901', '일반', '2024-08-16 08:00:00', NULL, NULL, 'https://demo-bucket-1222.s3.ap-northeast-2.amazonaws.com/images/b2.jpg', (SELECT id FROM ParkingSpot WHERE code = 'B2'));
INSERT INTO Vehicle (licensePlate, type, entryTime, exitTime, fee, s3, parking_spot_id) VALUES ('26누1965', '일반', '2024-08-16 08:00:00', NULL, NULL, 'https://demo-bucket-1222.s3.ap-northeast-2.amazonaws.com/images/c2.jpg', (SELECT id FROM ParkingSpot WHERE code = 'C2'));