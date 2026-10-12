docker build -t pricing-service:1.1.0 ./services/pricing-service
docker build -t allocation-service:1.0.0 ./services/allocation-service
docker images pricing-service allocation-service
